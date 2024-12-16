import { useEffect, useState } from "react";
import { getOrdenes } from "../services/api";

const Costos = () => {
  const [ordenes, setOrdenes] = useState([]); // Lista de órdenes
  const [error, setError] = useState(null);

  // Cargar las órdenes existentes desde el backend
  const cargarOrdenes = async () => {
    setError(null);
    try {
      const response = await getOrdenes();
      setOrdenes(response.data); // Almacenar las órdenes existentes
    } catch (err) {
      console.error("Error al cargar las órdenes:", err.message);
      setError("Error al cargar las órdenes. Verifique el servidor.");
    }
  };

  useEffect(() => {
    cargarOrdenes();
  }, []);

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Cálculo de Costos</h2>
      <p style={styles.subtitle}>
        Aquí puedes ver el desglose de los costos calculados para cada orden.
      </p>

      {error && <p style={styles.error}>{error}</p>}

      {/* Listado de órdenes con costos */}
      <h3 style={styles.sectionTitle}>Órdenes Existentes</h3>
      {ordenes.length > 0 ? (
        <table style={styles.table}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Usuario ID</th>
              <th>Producto ID</th>
              <th>Cantidad</th>
              <th>Costos Directos</th>
              <th>Costos Indirectos</th>
              <th>Costo Total</th>
            </tr>
          </thead>
          <tbody>
            {ordenes.map((orden) => (
              <tr key={orden.id}>
                <td>{orden.id}</td>
                <td>{orden.usuario_id}</td>
                <td>{orden.producto_id}</td>
                <td>{orden.cantidad}</td>
                <td>${orden.total_costos_directos?.toFixed(2)}</td>
                <td>${orden.total_costos_indirectos?.toFixed(2)}</td>
                <td>${orden.total_costos?.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No hay órdenes disponibles para mostrar.</p>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "900px",
    margin: "30px auto",
    padding: "20px",
    backgroundColor: "#444",
    borderRadius: "8px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
    color: "#fff",
  },
  title: {
    fontSize: "2rem",
    textAlign: "center",
    marginBottom: "10px",
  },
  subtitle: {
    fontSize: "1.2rem",
    textAlign: "center",
    marginBottom: "20px",
  },
  sectionTitle: {
    fontSize: "1.5rem",
    marginBottom: "10px",
    textAlign: "left",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    backgroundColor: "#fff",
    color: "#000",
  },
  th: {
    backgroundColor: "#28a745",
    color: "#fff",
    padding: "10px",
    textAlign: "left",
  },
  td: {
    padding: "10px",
    border: "1px solid #ccc",
    textAlign: "left",
  },
  error: {
    color: "red",
    marginTop: "10px",
    textAlign: "center",
  },
};

export default Costos;
