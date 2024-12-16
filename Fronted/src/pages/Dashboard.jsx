import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [usuario, setUsuario] = useState(null); // Guarda la info del usuario
  const navigate = useNavigate();

  // Obtener la información del usuario desde localStorage
  useEffect(() => {
    const usuarioGuardado = localStorage.getItem("usuario");
    if (usuarioGuardado) {
      setUsuario(usuarioGuardado);
    } else {
      navigate("/"); // Redirigir al login si no hay usuario
    }
  }, [navigate]);

  // Manejo del logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    navigate("/"); // Redirigir al login
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>¡Bienvenido, {usuario?.nombre || "Usuario"}! 👋</h2>
      <p style={styles.subtitle}>Selecciona una opción para empezar:</p>

      <div style={styles.grid}>
        <div style={styles.card} onClick={() => navigate("/costos")}>
          <h3>Cálculo de Costos</h3>
          <p>Calcula los costos de tus pedidos.</p>
        </div>

        <div style={styles.card} onClick={() => navigate("/ordenes")}>
          <h3>Gestión de Órdenes</h3>
          <p>Administra las órdenes existentes y crea nuevas.</p>
        </div>

        <div style={styles.card} onClick={() => navigate("/reportes")}>
          <h3>Reportes</h3>
          <p>Genera y descarga reportes en PDF.</p>
        </div>

        <div style={styles.card} onClick={() => navigate("/admin")}>
          <h3>Administración</h3>
          <p>Actualiza datos como productos y costos.</p>
        </div>
      </div>

      <button onClick={handleLogout} style={styles.logoutButton}>
        Cerrar Sesión
      </button>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "900px",
    margin: "30px auto",
    padding: "20px",
    textAlign: "center",
    backgroundColor: "#f9f9f9",
    borderRadius: "8px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
  },
  title: {
    fontSize: "2rem",
    marginBottom: "10px",
    color: "#333",
  },
  subtitle: {
    fontSize: "1.2rem",
    marginBottom: "20px",
    color: "#555",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "20px",
    marginBottom: "20px",
  },
  card: {
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    backgroundColor: "#000000",
    boxShadow: "0px 2px 4px rgba(0,0,0,0.1)",
    cursor: "pointer",
    transition: "transform 0.2s",
  },
  cardHover: {
    transform: "scale(1.05)",
  },
  logoutButton: {
    padding: "10px 20px",
    backgroundColor: "#dc3545",
    color: "#000000",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  },
};

export default Dashboard;
