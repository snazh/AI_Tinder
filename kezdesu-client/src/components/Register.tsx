// src/components/Register.tsx
const Register = () => {
  return (
    <div className="max-w-sm mx-auto mt-20 p-6 bg-white shadow rounded text-center">
      <h2 className="text-2xl font-semibold mb-4">Create an account</h2>
      <p className="text-gray-500 mb-6">Register with Google</p>
      <button
        onClick={() =>
          (window.location.href = "http://127.0.0.1:8000/auth/login")
        }
        className="flex items-center justify-center gap-2 w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
      >
        <img src="/google-icon.svg" alt="Google" className="w-5 h-5" />
        Register with Google
      </button>
    </div>
  );
};

export default Register;
