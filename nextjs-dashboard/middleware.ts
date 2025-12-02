import { withAuth } from 'next-auth/middleware';

// Only protect API routes, not pages (handled by PreLoader)
export default withAuth({
  pages: {
    signIn: '/login',
  },
});

export const config = {
  matcher: [
    '/api/protected/:path*',
  ],
};
