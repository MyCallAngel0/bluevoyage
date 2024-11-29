import "~/styles/globals.css";

import { Baloo_2 } from '@next/font/google';
import { type Metadata } from "next";

import TopNav from './components/Topnav';
import Footer from './components/footer';

export const metadata: Metadata = {
  title: "Blue Voyage",
  description: "Blue Voyage Travel Blog",
  icons: [{ rel: "icon", url: "/favicon.ico" }],
};

const baloo = Baloo_2({
  subsets: ["latin"],
  weight: ["400", "700"],
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div>
        {/* Add top navigation */}
        <TopNav />
        {children}

        {/* Add footer */}
        <Footer />
        </div> 
      </body>
    </html>
  );
}


