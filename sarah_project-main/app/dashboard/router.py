from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from sqlalchemy import func, case, extract, cast, Float

from .. import models, schemas
from ..database import get_db
from ..auth.utils import get_current_active_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=schemas.DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get a summary of the user's dashboard."""
    # Get total number of flashcard sets
    total_sets = (
        db.query(func.count(models.FlashcardSet.id))
        .filter(models.FlashcardSet.user_id == current_user.id)
        .scalar()
        or 0
    )

    # Get total number of flashcards
    total_cards = (
        db.query(func.count(models.Flashcard.id))
        .join(models.FlashcardSet, models.Flashcard.set_id == models.FlashcardSet.id)
        .filter(models.FlashcardSet.user_id == current_user.id)
        .scalar()
        or 0
    )

    # Get total number of study sessions
    total_study_sessions = (
        db.query(func.count(models.StudySession.id))
        .filter(models.StudySession.user_id == current_user.id)
        .scalar()
        or 0
    )

    # Calculate total study time in minutes
    total_study_time = (
        db.query(
            func.sum(
                func.julianday(
                    func.coalesce(
                        models.StudySession.end_time, func.current_timestamp()
                    )
                )
                - func.julianday(models.StudySession.start_time)
            )
            * 24
            * 60  # Convert to minutes
        )
        .filter(models.StudySession.user_id == current_user.id)
        .scalar()
        or 0
    )

    # Get mastered and struggling cards counts
    mastered_cards = 0
    struggling_cards = 0

    # Get all flashcards for the user
    user_flashcards = (
        db.query(models.Flashcard)
        .join(models.FlashcardSet, models.Flashcard.set_id == models.FlashcardSet.id)
        .filter(models.FlashcardSet.user_id == current_user.id)
        .all()
    )

    for flashcard in user_flashcards:
        # Get progress stats for this flashcard
        stats = models.FlashcardProgress.get_stats_by_flashcard(
            db, flashcard.id, current_user.id
        )

        if stats:
            if (
                stats.correct_count
                and stats.correct_count > 2
                and stats.average_difficulty
                and stats.average_difficulty < 2
            ):
                mastered_cards += 1
            elif stats.incorrect_count and stats.incorrect_count > stats.correct_count:
                struggling_cards += 1

    # Calculate completion percentage
    completion_percentage = 0
    if total_cards > 0:
        completion_percentage = (mastered_cards / total_cards) * 100

    return schemas.DashboardSummary(
        total_sets=total_sets,
        total_cards=total_cards,
        total_study_sessions=total_study_sessions,
        total_study_time_minutes=float(total_study_time),
        mastered_cards=mastered_cards,
        struggling_cards=struggling_cards,
        completion_percentage=completion_percentage,
    )


@router.get("/activity", response_model=List[schemas.ActivityItem])
def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get recent activity for the user."""
    activities = []

    # Get recent study sessions
    recent_sessions = (
        db.query(models.StudySession)
        .filter(models.StudySession.user_id == current_user.id)
        .order_by(models.StudySession.start_time.desc())
        .limit(limit)
        .all()
    )

    for session in recent_sessions:
        # Get the set title
        set_title = (
            db.query(models.FlashcardSet.title)
            .filter(models.FlashcardSet.id == session.set_id)
            .scalar()
            or "Unknown Set"
        )

        # Calculate duration if session is completed
        duration = "In progress"
        if session.end_time:
            # Ensure we get a positive duration
            time_diff = session.end_time - session.start_time
            minutes = abs(time_diff.total_seconds()) / 60
            duration = f"{minutes:.1f} minutes"

        activities.append(
            schemas.ActivityItem(
                id=session.id,
                type="study_session",
                timestamp=session.start_time,
                details={
                    "set_id": str(session.set_id),
                    "set_title": set_title,
                    "duration": duration,
                    "status": "Completed" if session.end_time else "In progress",
                },
            )
        )

    # Get recent flashcard set creations
    recent_sets = (
        db.query(models.FlashcardSet)
        .filter(models.FlashcardSet.user_id == current_user.id)
        .order_by(models.FlashcardSet.created_at.desc())
        .limit(limit)
        .all()
    )

    for flashcard_set in recent_sets:
        # Count cards in the set
        card_count = (
            db.query(func.count(models.Flashcard.id))
            .filter(models.Flashcard.set_id == flashcard_set.id)
            .scalar()
            or 0
        )

        activities.append(
            schemas.ActivityItem(
                id=flashcard_set.id,
                type="flashcard_set_created",
                timestamp=flashcard_set.created_at,
                details={
                    "set_id": str(flashcard_set.id),
                    "title": flashcard_set.title,
                    "card_count": str(card_count),
                },
            )
        )

    # Get recent flashcard progress
    recent_progress = (
        db.query(models.FlashcardProgress)
        .filter(models.FlashcardProgress.user_id == current_user.id)
        .order_by(models.FlashcardProgress.created_at.desc())
        .limit(limit)
        .all()
    )

    for progress in recent_progress:
        # Get the flashcard question
        flashcard = (
            db.query(models.Flashcard)
            .filter(models.Flashcard.id == progress.flashcard_id)
            .first()
        )

        if flashcard:
            # Get the set title
            set_title = (
                db.query(models.FlashcardSet.title)
                .join(
                    models.Flashcard, models.FlashcardSet.id == models.Flashcard.set_id
                )
                .filter(models.Flashcard.id == progress.flashcard_id)
                .scalar()
                or "Unknown Set"
            )

            activities.append(
                schemas.ActivityItem(
                    id=progress.id,
                    type="flashcard_progress",
                    timestamp=progress.created_at,
                    details={
                        "flashcard_id": str(progress.flashcard_id),
                        "question": flashcard.question,
                        "set_title": set_title,
                        "result": "Correct" if progress.is_correct else "Incorrect",
                        "difficulty": progress.difficulty,
                    },
                )
            )

    # Sort all activities by timestamp (newest first) and limit to requested number
    activities.sort(key=lambda x: x.timestamp, reverse=True)
    return activities[:limit]


@router.get("/sets/stats", response_model=List[schemas.SetStatistics])
def get_set_statistics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get statistics for all flashcard sets."""
    # Get all flashcard sets for the user
    user_sets = (
        db.query(models.FlashcardSet)
        .filter(models.FlashcardSet.user_id == current_user.id)
        .all()
    )

    set_stats = []

    for flashcard_set in user_sets:
        # Count total cards in the set
        total_cards = (
            db.query(func.count(models.Flashcard.id))
            .filter(models.Flashcard.set_id == flashcard_set.id)
            .scalar()
            or 0
        )

        # Get the last study session for this set
        last_session = (
            db.query(models.StudySession)
            .filter(
                models.StudySession.set_id == flashcard_set.id,
                models.StudySession.user_id == current_user.id,
            )
            .order_by(models.StudySession.start_time.desc())
            .first()
        )

        last_studied = last_session.start_time if last_session else None

        # Count study sessions for this set
        study_count = (
            db.query(func.count(models.StudySession.id))
            .filter(
                models.StudySession.set_id == flashcard_set.id,
                models.StudySession.user_id == current_user.id,
            )
            .scalar()
            or 0
        )

        # Calculate average session duration
        avg_duration = None
        if study_count > 0:
            avg_duration = (
                db.query(
                    func.avg(
                        func.julianday(
                            func.coalesce(
                                models.StudySession.end_time, func.current_timestamp()
                            )
                        )
                        - func.julianday(models.StudySession.start_time)
                    )
                    * 24
                    * 60  # Convert to minutes
                )
                .filter(
                    models.StudySession.set_id == flashcard_set.id,
                    models.StudySession.user_id == current_user.id,
                )
                .scalar()
            )

        # Calculate mastery percentage
        mastery_percentage = 0
        if total_cards > 0:
            # Get all flashcards in the set
            flashcards = (
                db.query(models.Flashcard)
                .filter(models.Flashcard.set_id == flashcard_set.id)
                .all()
            )

            mastered_count = 0
            for flashcard in flashcards:
                # Get progress stats for this flashcard
                stats = models.FlashcardProgress.get_stats_by_flashcard(
                    db, flashcard.id, current_user.id
                )

                if (
                    stats
                    and stats.correct_count
                    and stats.correct_count > 2
                    and stats.average_difficulty
                    and stats.average_difficulty < 2
                ):
                    mastered_count += 1

            mastery_percentage = (mastered_count / total_cards) * 100

        set_stats.append(
            schemas.SetStatistics(
                set_id=flashcard_set.id,
                title=flashcard_set.title,
                total_cards=total_cards,
                mastery_percentage=mastery_percentage,
                last_studied=last_studied,
                study_count=study_count,
                average_session_minutes=float(avg_duration) if avg_duration else None,
            )
        )

    return set_stats


@router.get("/study-time", response_model=schemas.StudyTimeDistribution)
def get_study_time_distribution(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get study time distribution by day, week, and month."""
    # Current date for reference
    now = datetime.now()

    # Daily distribution (last 7 days)
    daily_data = []
    for i in range(6, -1, -1):
        date = now - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")

        # Get study time for this day
        day_start = datetime(date.year, date.month, date.day, 0, 0, 0)
        day_end = datetime(date.year, date.month, date.day, 23, 59, 59)

        daily_minutes = (
            db.query(
                func.sum(
                    func.julianday(
                        func.min(
                            func.coalesce(
                                models.StudySession.end_time, func.current_timestamp()
                            ),
                            day_end,
                        )
                    )
                    - func.julianday(
                        func.max(models.StudySession.start_time, day_start)
                    )
                )
                * 24
                * 60  # Convert to minutes
            )
            .filter(
                models.StudySession.user_id == current_user.id,
                models.StudySession.start_time <= day_end,
                func.coalesce(models.StudySession.end_time, func.current_timestamp())
                >= day_start,
            )
            .scalar()
            or 0
        )

        daily_data.append(
            schemas.TimePoint(date=date_str, minutes=float(daily_minutes))
        )

    # Weekly distribution (last 4 weeks)
    weekly_data = []
    for i in range(3, -1, -1):
        week_start = now - timedelta(days=now.weekday() + 7 * i)
        week_end = week_start + timedelta(days=6)
        week_str = (
            f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}"
        )

        # Get study time for this week
        week_start_dt = datetime(
            week_start.year, week_start.month, week_start.day, 0, 0, 0
        )
        week_end_dt = datetime(week_end.year, week_end.month, week_end.day, 23, 59, 59)

        weekly_minutes = (
            db.query(
                func.sum(
                    func.julianday(
                        func.min(
                            func.coalesce(
                                models.StudySession.end_time, func.current_timestamp()
                            ),
                            week_end_dt,
                        )
                    )
                    - func.julianday(
                        func.max(models.StudySession.start_time, week_start_dt)
                    )
                )
                * 24
                * 60  # Convert to minutes
            )
            .filter(
                models.StudySession.user_id == current_user.id,
                models.StudySession.start_time <= week_end_dt,
                func.coalesce(models.StudySession.end_time, func.current_timestamp())
                >= week_start_dt,
            )
            .scalar()
            or 0
        )

        weekly_data.append(
            schemas.TimePoint(date=week_str, minutes=float(weekly_minutes))
        )

    # Monthly distribution (last 6 months)
    monthly_data = []
    for i in range(5, -1, -1):
        month_date = now - timedelta(days=30 * i)
        month_str = month_date.strftime("%Y-%m")

        # Get study time for this month
        month_start = datetime(month_date.year, month_date.month, 1, 0, 0, 0)
        if month_date.month == 12:
            month_end = datetime(month_date.year + 1, 1, 1, 0, 0, 0) - timedelta(
                seconds=1
            )
        else:
            month_end = datetime(
                month_date.year, month_date.month + 1, 1, 0, 0, 0
            ) - timedelta(seconds=1)

        monthly_minutes = (
            db.query(
                func.sum(
                    func.julianday(
                        func.min(
                            func.coalesce(
                                models.StudySession.end_time, func.current_timestamp()
                            ),
                            month_end,
                        )
                    )
                    - func.julianday(
                        func.max(models.StudySession.start_time, month_start)
                    )
                )
                * 24
                * 60  # Convert to minutes
            )
            .filter(
                models.StudySession.user_id == current_user.id,
                models.StudySession.start_time <= month_end,
                func.coalesce(models.StudySession.end_time, func.current_timestamp())
                >= month_start,
            )
            .scalar()
            or 0
        )

        monthly_data.append(
            schemas.TimePoint(date=month_str, minutes=float(monthly_minutes))
        )

    return schemas.StudyTimeDistribution(
        daily=daily_data, weekly=weekly_data, monthly=monthly_data
    )
