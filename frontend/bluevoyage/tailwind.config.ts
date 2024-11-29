import { type Config } from "tailwindcss";
import { fontFamily } from "tailwindcss/defaultTheme";

export default {
  content: ["./src/**/*.tsx"],
  theme: {
    extend: {
      fontFamily: {
        baloo: ['"Baloo 2"', ...fontFamily.sans], 
      },
    },
  },
  plugins: [],
} satisfies Config;
