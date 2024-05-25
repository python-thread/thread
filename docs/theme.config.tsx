import Image from "next/image";
import { useRouter } from "next/router";
import { useConfig } from "nextra-theme-docs";
import type { DocsThemeConfig } from "nextra-theme-docs";

import { Poppins } from "next/font/google";
const logoFont = Poppins({
  subsets: ["latin"],
  weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
  style: ["normal"],
});

const Logo = (
  <div className="flex flex-row gap-2 justify-center items-center">
    <Image
      width={32}
      height={32}
      src="/favicon-dark.png"
      alt=""
      className="hidden dark:flex"
    />
    <Image
      width={32}
      height={32}
      src="/favicon.png"
      alt=""
      className="flex dark:hidden"
    />
    <span
      className="text-xl font-bold text-black dark:text-white hover:text-black/95 dark:hover:text-white/95 transition-all"
      style={logoFont.style}
    >
      thread
    </span>
  </div>
);
const Footer = (
  <div className="flex w-full flex-col items-center sm:items-start">
    <div className="text-lg font-semibold">
      Your threading solution ♡⸜(˶˃ ᵕ ˂˶)⸝♡
    </div>
    <div className="mt-6 text-xs">
      Copyright (c) {new Date().getFullYear()}, thread.ngjx.org | All rights
      reserved
    </div>
  </div>
);
const Head = () => {
  const { title } = useConfig();
  const { route } = useRouter();

  const pageTitle =
    route === "/" || !title ? "Thread v2.0.2" : `${title} | Thread v2.0.2`;
  const socialImage = "https://thread.ngjx.org/socialcard-white.jpg";

  return (
    <>
      <meta name="msapplication-TileColor" content="#fff" />
      <meta name="theme-color" content="#fff" />

      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta httpEquiv="Content-Language" content="en" />

      {/* Icons */}
      <link rel="icon" href="/favicon.png" type="image/png" />
      <link rel="icon" href="/favicon.ico" type="image/x-icon" />
      <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      <link
        rel="icon"
        href="/favicon-dark.png"
        type="image/png"
        media="(prefers-color-scheme: dark)"
      />
      <link
        rel="icon"
        href="/favicon-dark.ico"
        type="image/x-icon"
        media="(prefers-color-scheme: dark)"
      />
      <link
        rel="icon"
        href="/favicon-dark.svg"
        type="image/svg+xml"
        media="(prefers-color-scheme: dark)"
      />

      {/* Description */}
      <meta
        name="description"
        content="Your python threading solution ♡⸜(˶˃ ᵕ ˂˶)⸝♡"
      />
      <meta
        name="og:description"
        content="Your python threading solution ♡⸜(˶˃ ᵕ ˂˶)⸝♡"
      />

      {/* OpenGraph */}
      <meta name="og:image" content={socialImage} />
      <meta name="og:title" content={pageTitle} />

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:image" content={socialImage} />
      <meta name="twitter:site:domain" content="thread.ngjx.org" />
      <meta name="twitter:url" content="https://thread.ngjx.org" />

      {/* Apple */}
      <meta name="apple-mobile-web-app-title" content="thread" />
    </>
  );
};

const config: DocsThemeConfig = {
  logo: Logo,
  head: Head,
  footer: { text: Footer },
  project: {
    link: "https://github.com/python-thread/thread",
  },
  docsRepositoryBase:
    "https://github.com/python-thread/thread.ngjx.org/tree/main",
  chat: {
    link: "https://discord.gg/WTAvycRmqP",
  },
  useNextSeoProps() {
    const { asPath } = useRouter();
    if (asPath !== "/") {
      return {
        titleTemplate: "%s | Thread v2.0.2",
      };
    }
  },
  sidebar: {
    defaultMenuCollapseLevel: 1,
    toggleButton: true,
  },
  toc: { backToTop: true },
};

export default config;
