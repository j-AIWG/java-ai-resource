// @ts-check
import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Java and AI',
  tagline: 'Java + AI Resource Hub',
  favicon: 'img/jAI.png',

  future: {
    v4: true,
  },

  url: 'https://lizeraes.github.io',
  baseUrl: '/ai-resource/',

  organizationName: 'lizeraes',
  projectName: 'java-ai-resource',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  trailingSlash: true,

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // ✅ Enable Mermaid plugin
  themes: ['@docusaurus/theme-mermaid'],

  // ✅ Enable Mermaid in Markdown
  markdown: {
    mermaid: true,
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: false, // Disable blog
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // ✅ Mermaid theme setup
      mermaid: {
        theme: {
          light: 'neutral',
          dark: 'forest',
        },
      },
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Java and AI',
        logo: {
          alt: 'jAI Logo',
          src: 'img/jAI.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Contents',
          },
          {
            href: 'https://github.com/facebook/docusaurus',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Contents',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'X',
                href: 'https://x.com/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/facebook/docusaurus',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Java and AI Resource Hub. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
