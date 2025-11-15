import React, { useState } from "react";
import { createProfile } from "../api/profile.api";

export default function ProfileCreator() {
  const [avatar, setAvatar] = useState<File | null>(null);
  const [name, setName] = useState("");
  const [bio, setBio] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!avatar) return alert("Please upload an avatar");

    try {
      const token = localStorage.getItem("access_token")!;
      const result = await createProfile(
        {
          name,
          bio,
          age: 25, // пример
        },
        avatar,
        token
      );

      console.log("Profile created:", result);
      alert("Profile created!");
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Name"
        onChange={(e) => setName(e.target.value)}
      />

      <input
        type="text"
        placeholder="Bio"
        onChange={(e) => setBio(e.target.value)}
      />

      <input
        type="file"
        onChange={(e) => setAvatar(e.target.files?.[0] || null)}
      />

      <button type="submit">Create Profile</button>
    </form>
  );
}
