// pages/login.tsx
'use client';
import { useState, type ChangeEvent, type FormEvent } from 'react';

interface LoginFormData {
  username: string;
  password: string;
  otp: string;
}

const LoginPage = () => {
  const [formData, setFormData] = useState<LoginFormData>({
    username: '',
    password: '',
    otp: '',
  });
  const [isOtpSent, setIsOtpSent] = useState<boolean>(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!isOtpSent) {
      // Handle regular login
      const response = await fetch('http://localhost:8000/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setIsOtpSent(true);
        alert('OTP sent! Please check your email.');
      } else {
        const errorData = await response.json() as { detail: string };
        alert(`Error: ${errorData.detail}`);
      }
    } else {
      // Handle OTP verification
      const response = await fetch('http://localhost:8000/api/verify-otp/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        alert('Login successful!');
      } else {
        const errorData = await response.json() as { detail: string };
        alert(`Error: ${errorData.detail}`);
      }
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          placeholder="Username or Email"
        />
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Password"
        />
        {isOtpSent && (
          <input
            type="text"
            name="otp"
            value={formData.otp}
            onChange={handleChange}
            placeholder="Enter OTP"
          />
        )}
        <button type="submit">{isOtpSent ? 'Verify OTP' : 'Login'}</button>
      </form>
    </div>
  );
};

export default LoginPage;
