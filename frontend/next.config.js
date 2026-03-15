/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Enable standalone output for Docker
  output: 'standalone',

  // Transpile ESM-only packages for SSR compatibility
  transpilePackages: [
    'react-markdown',
    'remark-parse',
    'remark-rehype',
    'unified',
    'unist-util-visit',
    'unist-util-visit-parents',
    'unist-util-is',
    'unist-util-position',
    'vfile',
    'vfile-message',
    'hast-util-to-jsx-runtime',
    'hast-util-whitespace',
    'hast-util-is-element',
    'mdast-util-to-hast',
    'mdast-util-definitions',
    'html-url-attributes',
    'devlop',
    'micromark',
    'micromark-core-commonmark',
    'micromark-factory-destination',
    'micromark-factory-label',
    'micromark-factory-space',
    'micromark-factory-title',
    'micromark-factory-whitespace',
    'micromark-util-character',
    'micromark-util-chunked',
    'micromark-util-classify-character',
    'micromark-util-combine-extensions',
    'micromark-util-decode-numeric-character-reference',
    'micromark-util-decode-string',
    'micromark-util-encode',
    'micromark-util-html-tag-name',
    'micromark-util-normalize-identifier',
    'micromark-util-resolve-all',
    'micromark-util-sanitize-uri',
    'micromark-util-subtokenize',
    'micromark-util-symbol',
    'micromark-util-types',
    'mdast-util-from-markdown',
    'mdast-util-to-markdown',
    'ccount',
    'decode-named-character-reference',
    'character-entities',
    'property-information',
    'space-separated-tokens',
    'comma-separated-tokens',
  ],

  // Optimize images
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
    ],
    formats: ['image/webp', 'image/avif'],
  },

  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ];
  },

  // Webpack configuration
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }
    return config;
  },
};

module.exports = nextConfig;
