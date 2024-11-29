'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { FaGoogle } from 'react-icons/fa';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [otp, setOtp] = useState<string>('');
  const [step, setStep] = useState<number>(1); // Step 1: Login, Step 2: OTP
  const [errorMessage, setErrorMessage] = useState<string>('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include',
      });

      if (!response.ok) throw new Error('Login failed');

      const data = await response.json() as { jwt: string };

      if (data.jwt) {
        // Redirect after successful login
        router.push('/');
      } else {
        // Proceed to OTP verification
        setStep(2);
      }
    } catch (error) {
      setErrorMessage((error as Error).message);
    }
  };

  const handleOtpVerification = async () => {
    setErrorMessage('');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/verify-otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, otp }),
        credentials: 'include',
      });

      if (!response.ok) throw new Error('OTP verification failed');
      console.log('OTP verification successful');

      // Redirect after successful OTP verification
      router.push('/');
    } catch (error) {
      setErrorMessage((error as Error).message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center login-container">
      <div className="w-[450px] bg-transparent text-white rounded-lg p-8">
        {step === 1 ? (
          // Step 1: Login Form
          <form onSubmit={handleLogin}>
            <h1 className="text-5xl text-center mb-6">BlueVoyage</h1>
            <div className="mb-4">
              <input
                type="text"
                placeholder="Email"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full p-3 border border-white rounded-lg text-black"
              />
            </div>
            <div className="mb-4">
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full p-3 border border-white rounded-lg text-black"
              />
            </div>
            <p className="text-xs text-center mb-4">
              By clicking Log In, you agree to BlueVoyage’s{' '}
              <Link href="/terms" className="underline">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link href="/privacy" className="underline">
                Privacy Policy
              </Link>
              .
            </p>
            <button
              type="submit"
              className="w-full p-3 bg-gray-800 hover:bg-gray-700 rounded-lg text-white font-semibold"
            >
              Log in
            </button>
            <div className="flex justify-center mt-4">
              <Link href="/forgot-password" className="text-sm underline">
                Forgot your password?
              </Link>
            </div>
            <div className="flex items-center my-6">
              <div className="flex-1 h-px bg-white"></div>
              <span className="px-3">or</span>
              <div className="flex-1 h-px bg-white"></div>
            </div>
            <button
              type="button"
              className="flex items-center justify-center w-full p-3 bg-white text-gray-700 font-semibold rounded-lg gap-2"
            >
              <FaGoogle />
              Continue with Google
            </button>
            <p className="text-sm text-center mt-4">
              Don&apos;t have an account?{' '}
              <Link href="/signup" className="underline font-semibold">
                Sign up!
              </Link>
            </p>
          </form>
        ) : (
          // Step 2: OTP Verification
          <div>
            <h2 className="text-2xl text-center mb-6">Enter OTP</h2>
            <input
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              required
              className="w-full p-3 mb-4 border border-white rounded-lg text-black"
            />
            <button
              type="button"
              onClick={handleOtpVerification}
              className="w-full p-3 bg-gray-800 hover:bg-gray-700 rounded-lg text-white font-semibold"
            >
              Verify OTP
            </button>
          </div>
        )}
        {errorMessage && (
          <p className="text-red-500 text-center mt-4">{errorMessage}</p>
        )}
      </div>
    </div>
  );
};

export default LoginPage;
