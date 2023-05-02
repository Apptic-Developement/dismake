// imports 
import { useConfig } from 'nextra-theme-docs'

// theme config
export default {
  logo: <strong>Dismake</strong>,
  logoLink: "/",
  project: {
    link: "https://github.com/PranoyMajumdar/dismake",
  },
  docsRepositoryBase: "https://github.com/PranoyMajumdar/dismake/docs/pages",
  chat: {
    link: "https://dsc.gg/apptic",
  },
  useNextSeoProps() {
    return {
      titleTemplate: "%s | Dismake Docs",
    };
  },
  banner: {
    key: "dismake-dev",
    dismissible: true,
    text: (
      <a href="https://github.com/PranoyMajumdar/dismake/pulls" target="_blank">
        💖 Contribute now →
      </a>
    ),
  },
  footer: {
    text: (
      <span>
        MIT {new Date().getFullYear()} ©{" "}
        <a href="https://github.com/PranoyMajumdar/dismake" target="_blank">
          Apptic Development
        </a>
        .
      </span>
    ),
  },
  head: function useHead() {
    const { title } = useConfig();
    return (
      <>
        <meta
          name="description"
          content="Dismake is a robust framework designed to assist you in developing stateless and independent Discord bots that employ Slash Commands. The framework is built on top of the FastAPI, a high-performance Python web framework, making it easy to use, efficient, and speedy."
        />
        <meta
          name="og:description"
          content="Dismake is a robust framework designed to assist you in developing stateless and independent Discord bots that employ Slash Commands. The framework is built on top of the FastAPI, a high-performance Python web framework, making it easy to use, efficient, and speedy."
        />
        <meta name="og:title" content={title} />
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </>
    );
  },
};
