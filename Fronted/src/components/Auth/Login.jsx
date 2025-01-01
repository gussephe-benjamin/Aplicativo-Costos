import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../../services/api";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Limpiar errores previos

    try {
      const data = { email, contraseña: password };
      const response = await login(data); // Llamada a la API desde services/api.js

      // Guardar el token JWT en el localStorage
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("usuario", JSON.stringify(response.data.usuario));

      // Redirigir al Dashboard
      navigate("/dashboard");
    } catch (error) {
      console.error("Error en el login:", error.message);
      setError("Error al iniciar sesión. Verifica tus credenciales.");
    }
  };

  return (
    <div style={styles.container}>
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        {error && <p style={styles.error}>{error}</p>}

        <label>Email:</label>
        <input
          type="email"
          placeholder="ejemplo@correo.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label>Contraseña:</label>
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit" style={styles.button}>
          Iniciar Sesión
        </button>
      </form>

      <p style={styles.registerLink}>
        ¿No tienes una cuenta?{" "}
        <a href="/register" style={{ textDecoration: "none", color: "#007bff" }}>
          Regístrate aquí
        </a>
      </p>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "400px",
    margin: "50px auto",
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "5px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
    backgroundColor: "#f9f9f9",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  button: {
    backgroundColor: "#00000",
    color: "white",
    padding: "10px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  },
  error: { color: "red", marginBottom: "10px" },
  registerLink: { textAlign: "center", marginTop: "10px" },
};

export default Login;
