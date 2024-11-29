// /app/home/page.tsx

import "~/styles/globals.css";
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg bg-gradient-to-b from-[#03045E] to-[#0077B6] text-white p-4">
      {/* Introduction Section */}
      <section className="text-center mb-12">
        <h1 className="mainPage-headers">Welcome to Blue Voyage!</h1>
        <p className="mainPage-text">
          A place to share your travel adventures, tips, and experiences with fellow travelers. Join us and start posting your journeys!
        </p>
      </section>

      {/* Buttons Section */}
      <section className="flex gap-6">
        {/* Create Post Button */}
        <Link
          href="/create-post"
          className="create-post"
        >
          Create Post
        </Link>
        {/* Sign Up Button */}
        <Link
          href="/signup"
          className="signup"
        >
          Sign Up
        </Link>
      </section>
    </main>
  );
}
