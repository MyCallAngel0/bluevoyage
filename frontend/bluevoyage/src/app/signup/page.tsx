'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { FaGoogle } from 'react-icons/fa';
import Link from 'next/link';

const SignupPage: React.FC = () => {
  const [firstName, setFirstName] = useState<string>('');
  const [lastName, setLastName] = useState<string>('');
  const [username, setUsername] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [successMessage, setSuccessMessage] = useState<string>('');

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          username,
          email,
          password,
        }),
      });

      if (!response.ok) {
        throw new Error('Registration failed');
      }

      const data = await response.json() as { message: string };
      console.log(data.message);
      setSuccessMessage('Verification token sent to your email!');
      setFirstName('');
      setLastName('');
      setUsername('');
      setEmail('');
      setPassword('');

      // Redirect after successful signup
      router.push('/');
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'An unknown error occurred');
    }
  };

  return (
    <div className="flex justify-center items-center h-screen signup-container">
      <div className="register-container bg-transparent p-8 rounded-2xl shadow-xl">

        <form onSubmit={handleSubmit}>
          <div className="input-firstname mb-4">
            <input
              type="text"
              placeholder="First Name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
              className="w-full p-3 rounded-md border-2 border-gray-200"
            />
          </div>
          <div className="input-lastname mb-4">
            <input
              type="text"
              placeholder="Last Name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
              className="w-full p-3 rounded-md border-2 border-gray-200"
            />
          </div>
          <div className="input-username mb-4">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full p-3 rounded-md border-2 border-gray-200"
            />
          </div>
          <div className="input-email mb-4">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full p-3 rounded-md border-2 border-gray-200"
            />
          </div>
          <div className="input-box mb-6">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full p-3 rounded-md border-2 border-gray-200"
            />
          </div>
          <button type="submit" className="signup-button bg-green-600 text-white p-3 w-full rounded-lg">
            Sign up
          </button>
        </form>

        {errorMessage && <p className="text-red-500 mt-4">{errorMessage}</p>}
        {successMessage && <p className="text-green-500 mt-4">{successMessage}</p>}

        <div className="login-message text-center mt-4">
          <Link href="/login" className="text-white hover:underline">Already have an account? Log in!</Link>
        </div>

        <div className="or-container flex justify-center my-8">
          <div className="line flex-1 h-px bg-white"></div>
          <span className="or text-white mx-4">or</span>
          <div className="line flex-1 h-px bg-white"></div>
        </div>

        <div className="continue">
          <button className="google-signin-button flex items-center justify-center gap-4 w-full py-3 bg-white border border-gray-200 rounded-lg">
            <FaGoogle />
            <span>Continue with Google</span>
          </button>
        </div>

        <div className="bottom-links fixed bottom-4 left-4 text-white flex gap-4">
          <a href="#" target="_blank" rel="noopener noreferrer">Terms</a>
          <a href="#" target="_blank" rel="noopener noreferrer">Privacy</a>
          <a href="#" target="_blank" rel="noopener noreferrer">Support</a>
          <a href="#" target="_blank" rel="noopener noreferrer">Information</a>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
