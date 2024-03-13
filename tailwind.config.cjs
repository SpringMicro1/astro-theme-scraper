module.exports = {
  content: ["./src/**/*.{astro,html,js,jsx,md,svelte,ts,tsx,vue}"],
  theme: {
    fontFamily: {
      junction: "Junction",
    },
    extend: {
      // Extend the 'prose' theme object
      prose: {
        // Specify the color for links
        links: {
          color: "blue-500", // You can also use 'blue-500' if you prefer
        },
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
