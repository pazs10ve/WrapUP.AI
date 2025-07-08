import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  webpack: (config, { isServer }) => {
    // Exclude puppeteer-extra and its plugins from being bundled on the server
    if (isServer) {
      config.externals = [...config.externals, 'puppeteer-extra', 'puppeteer-extra-plugin-stealth'];
    }

    return config;
  },
};

export default nextConfig;
