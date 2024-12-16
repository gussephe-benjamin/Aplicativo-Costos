import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();

  // Manejar el cierre de sesión
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    navigate("/"); // Redirige al login
  };

  return (
    <nav style={styles.navbar}>
      <div style={styles.logo}>
        <h2>Aplicación de Costos</h2>
      </div>
      <ul style={styles.navLinks}>
        <li>
          <Link to="/dashboard" style={styles.link}>
            Dashboard
          </Link>
        </li>
        <li>
          <Link to="/costos" style={styles.link}>
            Cálculo de Costos
          </Link>
        </li>
        <li>
          <Link to="/ordenes" style={styles.link}>
            Gestión de Órdenes
          </Link>
        </li>
        <li>
          <Link to="/reportes" style={styles.link}>
            Reportes
          </Link>
        </li>
        <li>
          <Link to="/admin" style={styles.link}>
            Administración
          </Link>
        </li>
      </ul>
      <button onClick={handleLogout} style={styles.logoutButton}>
        Cerrar Sesión
      </button>
    </nav>
  );
};

const styles = {
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#007bff",
    padding: "10px 20px",
    color: "#fff",
    boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.1)",
  },
  logo: {
    fontSize: "1.5rem",
  },
  navLinks: {
    display: "flex",
    listStyle: "none",
    gap: "20px",
    margin: 0,
    padding: 0,
  },
  link: {
    color: "#fff",
    textDecoration: "none",
    fontSize: "1rem",
    transition: "color 0.3s",
  },
  linkHover: {
    color: "#ffcc00",
  },
  logoutButton: {
    backgroundColor: "#dc3545",
    color: "#fff",
    border: "none",
    padding: "8px 12px",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "1rem",
    transition: "background-color 0.3s",
  },
};

export default Navbar;
