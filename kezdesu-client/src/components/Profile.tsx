// Profile.tsx
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

const Profile = () => {
  const { user } = useContext(AuthContext);
  if (!user) return <p>Not authenticated</p>;

  return (
    <div>
      <h2>{user.name}</h2>
      {user.picture && <img src={user.picture} alt="User profile" />}
    </div>
  );
};

export default Profile; // ✅ главное: экспо  рт компонента
