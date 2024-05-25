/** @type {import('nextra').withNextra} */
const withNextra = require("nextra")({
  theme: "nextra-theme-docs",
  themeConfig: "./theme.config.tsx",
  defaultShowCopyCode: true,
  latex: true,
});

/** @type {import('next').NextConfig} */
const NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "avatars.githubusercontent.com",
        pathname: "/u/*",
      },
    ],
  },
  redirects: async () => [
    {
      source: "/docs/v2:any?/:path*",
      destination: "/docs/latest/:path*",
      permanent: false,
    },
    {
      source: "/docs/v:major.:minor.:patch/:path*",
      destination: "/docs/v:major/:path*",
      permanent: true,
    },
    {
      source: "/github/v:major.:minor.:patch/:path*",
      destination:
        "https://github.com/python-thread/thread/releases/tag/v:major.:minor.:patch",
      permanent: true,
    },
  ],
};

module.exports = withNextra(NextConfig);
