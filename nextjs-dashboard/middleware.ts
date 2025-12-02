export { default } from 'next-auth/middleware';

export const config = {
  matcher: [
    '/',
    '/indicators/:path*',
    '/tract-explorer/:path*',
    '/scenario-analysis/:path*',
    '/recommendations/:path*',
  ],
};
