'use client';

import "~/styles/globals.css";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

export default function SettingsPage() {
  const router = useRouter();

  // Mock current user data
  const [userName, setUserName] = useState('Alice');
  const [userEmail, setUserEmail] = useState('alice@example.com');
  const [userPhoto, setUserPhoto] = useState<string | ArrayBuffer | null>(null); // For storing the profile photo
  const [newUserName, setNewUserName] = useState('');
  const [newUserEmail, setNewUserEmail] = useState('');
  const [newFirstName, setNewFirstName] = useState('');
  const [newLastName, setNewLastName] = useState('');
  const [loading, setLoading] = useState(false); // Track loading state
  const [error, setError] = useState<string | null>(null); // Track error state

  // Handle the file input for profile photo
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setUserPhoto(reader.result); // Set the photo data to be displayed
      };
      reader.readAsDataURL(file); // Read the file as a data URL (base64)
    }
  };

  // Handle the settings save
  const handleSaveSettings = async () => {
    setLoading(true); // Show loading state
    setError(null); // Clear any previous errors

    try {
      // Prepare form data
      const formData = new FormData();
      formData.append('username', newUserName || userName);
      formData.append('email', newUserEmail || userEmail);
      if (newFirstName) formData.append('first_name', newFirstName);
      if (newLastName) formData.append('last_name', newLastName);
      if (userPhoto) formData.append('photo', userPhoto as string);

      // Send the data to the backend
      const response = await fetch('http://localhost:8000/api/update_profile', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      const result = await response.json() as { username: string; email: string };
      console.log('Profile updated successfully:', result);

      // Update local state with new values
      setUserName(newUserName || userName);
      setUserEmail(newUserEmail || userEmail);

      alert('Profile updated successfully!');
      router.push('/profile'); // Navigate to the profile page
    } catch (err) {
      console.error('Error updating profile:', err);
      setError('Failed to update profile. Please try again.');
    } finally {
      setLoading(false); // Hide loading state
    }
  };

  return (
    <main className="min-h-screen p-6 bg-gradient-to-b from-[#03045E] to-[#0077B6]">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Profile Settings</h1>

        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-2xl font-semibold mb-4">Update Profile</h2>

          {/* Profile Photo */}
          <div className="mb-6">
            <label className="block text-gray-700">Profile Photo</label>
            <div className="flex items-center space-x-4">
              <div className="w-24 h-24 rounded-full overflow-hidden bg-gray-200 flex justify-center items-center">
                {userPhoto ? (
                  <Image
                    src={userPhoto as string}
                    alt="Profile Photo"
                    width={100}
                    height={100}
                  />
                ) : (
                  <span className="text-gray-400">No Photo</span>
                )}
              </div>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="border border-gray-300 rounded p-2"
              />
            </div>
          </div>

          {/* First Name */}
          <div className="mb-4">
            <label className="block text-gray-700">First Name</label>
            <input
              type="text"
              value={newFirstName}
              onChange={(e) => setNewFirstName(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Enter your first name"
            />
          </div>

          {/* Last Name */}
          <div className="mb-4">
            <label className="block text-gray-700">Last Name</label>
            <input
              type="text"
              value={newLastName}
              onChange={(e) => setNewLastName(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Enter your last name"
            />
          </div>

          {/* Username */}
          <div className="mb-4">
            <label className="block text-gray-700">Username</label>
            <input
              type="text"
              value={newUserName || userName}
              onChange={(e) => setNewUserName(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Enter your username"
            />
          </div>

          {/* Email */}
          <div className="mb-4">
            <label className="block text-gray-700">Email</label>
            <input
              type="email"
              value={newUserEmail || userEmail}
              onChange={(e) => setNewUserEmail(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Enter your email"
            />
          </div>

          {/* Save Settings Button */}
          <button
            onClick={handleSaveSettings}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? 'Saving...' : 'Save Settings'}
          </button>
          {error && <p className="text-red-500 mt-4">{error}</p>}
        </div>
      </div>
    </main>
  );
}
