const Login = () => {
  const login = () => {
    globalThis.location.href = "http://127.0.0.1:8000/auth/login";
  };

  return <button onClick={login}>Login with Google</button>;
};

export default Login;
