# Flashcard App Frontend

This is the frontend for the Flashcard App, built with Next.js, TypeScript, and Tailwind CSS.

## Prerequisites

- Node.js 18.x or later
- npm or yarn

## Getting Started

1. Install dependencies:

```bash
npm install
# or
yarn install
```

2. Run the development server:

```bash
npm run dev
# or
yarn dev
```

3. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Project Structure

- `src/app`: Contains the Next.js app router pages and layouts
- `src/components`: Reusable UI components
- `src/services`: API services for backend communication
- `src/hooks`: Custom React hooks
- `src/lib`: Utility functions and helpers
- `src/types`: TypeScript type definitions

## Features

- User authentication (login/signup)
- Dashboard with study statistics
- Flashcard set management
- Study sessions
- Document upload and AI-powered flashcard generation
- Progress tracking

## Backend Integration

The frontend is configured to communicate with the backend API running at `http://localhost:8080/api`. This is set up in the `next.config.js` file using the rewrites feature.

Make sure the backend server is running before using the frontend application.

## Deployment

To build the application for production:

```bash
npm run build
# or
yarn build
```

Then, you can start the production server:

```bash
npm run start
# or
yarn start
```

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
