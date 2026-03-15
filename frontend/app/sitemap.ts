import { MetadataRoute } from "next";

const BASE = "https://tramitup.com";

const seoLandings = [
  { path: "/reclamar-vuelo-cancelado", priority: 0.8 },
  { path: "/reclamar-vuelo-retrasado", priority: 0.8 },
  { path: "/modelo-carta-reclamacion-aerolinea", priority: 0.8 },
  { path: "/reclamar-factura-luz-incorrecta", priority: 0.8 },
  { path: "/modelo-carta-finiquito", priority: 0.8 },
  { path: "/calcular-finiquito", priority: 0.8 },
  { path: "/reclamar-fianza-piso", priority: 0.8 },
  { path: "/modelo-carta-reclamacion-banco", priority: 0.8 },
  { path: "/recurrir-multa-trafico", priority: 0.8 },
  { path: "/reclamacion-seguridad-social", priority: 0.8 },
  { path: "/recurso-reposicion-hacienda", priority: 0.8 },
];

export default function sitemap(): MetadataRoute.Sitemap {
  const staticPages: MetadataRoute.Sitemap = [
    { url: BASE, lastModified: new Date(), changeFrequency: "weekly", priority: 1 },
    { url: `${BASE}/pricing`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.9 },
    { url: `${BASE}/login`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.7 },
    { url: `${BASE}/aviso-legal`, lastModified: new Date(), changeFrequency: "yearly", priority: 0.5 },
    { url: `${BASE}/privacidad`, lastModified: new Date(), changeFrequency: "yearly", priority: 0.5 },
    { url: `${BASE}/terminos`, lastModified: new Date(), changeFrequency: "yearly", priority: 0.5 },
  ];

  const landingPages: MetadataRoute.Sitemap = seoLandings.map(({ path, priority }) => ({
    url: `${BASE}${path}`,
    lastModified: new Date(),
    changeFrequency: "monthly" as const,
    priority,
  }));

  return [...staticPages, ...landingPages];
}
