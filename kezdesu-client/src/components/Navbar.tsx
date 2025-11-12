// src/components/Navbar.tsx
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { logoutApi } from "../api/auth.api";

const Navbar = () => {
  const { user, setUser } = useContext(AuthContext);

  const logout = async () => {
    await logoutApi();
    setUser(null);
  };

  return (
    <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
      <h1 className="font-bold text-xl text-gray-800">KezdesuAI</h1>
      <div className="flex items-center gap-4">
        {user ? (
          <>
            <span className="text-gray-700">{user.name}</span>
            {user.picture && (
              <img
                src={user.picture}
                alt="avatar"
                className="w-8 h-8 rounded-full"
              />
            )}
            <button
              onClick={logout}
              className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
            >
              Logout
            </button>
          </>
        ) : (
          <a
            href="/auth"
            className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition"
          >
            Login
          </a>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
