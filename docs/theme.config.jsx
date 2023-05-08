// imports
import { useConfig } from "nextra-theme-docs";
import Image from "next/image";
import { useMounted } from "nextra/hooks";
import { useTheme } from "next-themes";

// theme config
export default {
  logo: function Logo() {
    // get theme
    let mounted = useMounted();
    let theme = mounted && useTheme().resolvedTheme;

    return (
      <>
        <Image
          style={{
            filter: `brightness(${
              theme == "light" ? "100" : "0"
            }) saturate(100%) invert(100%)`,
          }}
          width={32}
          height={32}
          alt="Logo"
          src="/logo.png "
        />
        <span>
          <strong>Dismake</strong>
        </span>
      </>
    );
  },
  logoLink: "/",
  project: {
    link: "https://github.com/Apptic-Developement/dismake",
  },
  docsRepositoryBase: "https://github.com/Apptic-Developement/dismake/docs/pages",
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
      <a href="https://github.com/Apptic-Developement/dismake/pulls" target="_blank">
        💖 Contribute now →
      </a>
    ),
  },
  footer: {
    text: (
      <span>
        MIT {new Date().getFullYear()} ©{" "}
        <a href="https://github.com/Apptic-Developement/dismake" target="_blank">
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
        <link rel="icon" href="/logo.png" type="image/svg+xml" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </>
    );
  },
};
