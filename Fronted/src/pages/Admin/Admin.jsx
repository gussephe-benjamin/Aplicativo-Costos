import { Link } from "react-router-dom";

const Admin = () => {
  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Administración de Datos</h2>
      <p style={styles.subtitle}>Selecciona una categoría para gestionar:</p>

      <div style={styles.grid}>
        {/* Administración de Productos */}
        <div style={styles.card}>
          <h3>Productos</h3>
          <p>Gestiona los modelos de productos.</p>
          <Link to="/admin/productos" style={styles.button}>
            Ir a Productos
          </Link>
        </div>

        {/* Administración de Mano de Obra */}
        <div style={styles.card}>
          <h3>Mano de Obra</h3>
          <p>Administra los datos de la mano de obra.</p>
          <Link to="/admin/mano-obra" style={styles.button}>
            Ir a Mano de Obra
          </Link>
        </div>

        {/* Administración de Materia Prima */}
        <div style={styles.card}>
          <h3>Materia Prima</h3>
          <p>Gestiona los insumos necesarios para los pedidos.</p>
          <Link to="/admin/materia-prima" style={styles.button}>
            Ir a Materia Prima
          </Link>
        </div>

        {/* Administración de Costos Indirectos */}
        <div style={styles.card}>
          <h3>Costos Indirectos</h3>
          <p>Administra los costos generales (electricidad, maquinaria, etc.).</p>
          <Link to="/admin/costos-indirectos" style={styles.button}>
            Ir a Costos Indirectos
          </Link>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "800px",
    margin: "30px auto",
    padding: "20px",
    textAlign: "center",
    backgroundColor: "#f9f9f9",
    borderRadius: "8px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
  },
  title: { fontSize: "2rem", marginBottom: "10px", color: "#333" },
  subtitle: { fontSize: "1.2rem", marginBottom: "20px", color: "#555" },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "20px",
  },
  card: {
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    backgroundColor: "#fff",
    boxShadow: "0px 2px 4px rgba(0,0,0,0.1)",
    textAlign: "left",
  },
  button: {
    display: "inline-block",
    marginTop: "10px",
    padding: "10px 20px",
    backgroundColor: "#007bff",
    color: "#fff",
    borderRadius: "5px",
    textDecoration: "none",
    textAlign: "center",
  },
};

export default Admin;
