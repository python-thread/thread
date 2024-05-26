/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl:
    process.env.NODE_ENV === "production"
      ? "https://thread.ngjx.org"
      : "http://localhost:3000",
  generateRobotsTxt: true, // (optional)
  // ...other options
};
