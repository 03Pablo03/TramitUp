import { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/chat", "/account", "/documents", "/alerts", "/onboarding"],
    },
    sitemap: "https://tramitup.com/sitemap.xml",
  };
}
