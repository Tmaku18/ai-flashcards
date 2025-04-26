/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "standalone",
  // Skip TypeScript checking in production builds if environment variable is set
  typescript: {
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    ignoreBuildErrors: process.env.SKIP_TYPECHECK === "true",
  },
  // Configure proxy for API requests
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        // Use backend service name when running in Docker
        destination: process.env.NEXT_PUBLIC_API_URL
          ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`
          : "http://localhost:8080/api/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
