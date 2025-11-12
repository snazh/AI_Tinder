// src/pages/Home.tsx
import { useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import { getMe } from "../api/auth.api";

const Home = () => {
  const { user, setUser } = useContext(AuthContext);

  useEffect(() => {
    const fetchUser = async () => {
      const me = await getMe();
      if (me) setUser(me);
    };
    fetchUser();
  }, [setUser]);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Welcome to KezdesuAI!</h1>
      {user ? (
        <div className="p-6 bg-white shadow rounded max-w-md">
          <img
            src={user.picture}
            alt="profile"
            className="w-24 h-24 rounded-full mx-auto"
          />
          <h2 className="text-xl font-semibold mt-4 text-center">
            {user.name}
          </h2>
          <p className="text-gray-600 text-center">{user.email}</p>
        </div>
      ) : (
        <p className="text-gray-500">Please log in to see your profile.</p>
      )}
    </div>
  );
};

export default Home;
