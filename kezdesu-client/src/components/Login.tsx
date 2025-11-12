// src/components/Login.tsx
const Login = () => {
  const login = () => {
    globalThis.location.href = "http://127.0.0.1:8000/auth/login";
  };

  return (
    <div className="max-w-sm mx-auto mt-20 p-6 bg-white shadow rounded text-center">
      <h2 className="text-2xl font-semibold mb-4">Welcome back!</h2>
      <p className="text-gray-500 mb-6">Login with your Google account</p>
      <button
        onClick={login}
        className="flex items-center justify-center gap-2 w-full bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
      >
        <img src="/google-icon.svg" alt="Google" className="w-5 h-5" />
        Login with Google
      </button>
    </div>
  );
};

export default Login;
