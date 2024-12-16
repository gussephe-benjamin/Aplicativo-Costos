import { useEffect, useState } from "react";
import { getOrdenes, descargarReportePDF } from "../services/api";

const Reportes = () => {
  const [ordenes, setOrdenes] = useState([]); // Lista de órdenes
  const [mensaje, setMensaje] = useState(null);
  const [error, setError] = useState(null);

  // Cargar todas las órdenes desde el backend
  const cargarOrdenes = async () => {
    setError(null);
    try {
      const response = await getOrdenes();
      setOrdenes(response.data);
    } catch (err) {
      console.error("Error al cargar órdenes:", err.message);
      setError("Error al cargar las órdenes.");
    }
  };

  useEffect(() => {
    cargarOrdenes();
  }, []);

  // Descargar el PDF para una orden específica
  const handleDescargarPDF = async (orden_id) => {
    setError(null);
    setMensaje(null);

    try {
      const response = await descargarReportePDF(orden_id);

      // Crear un objeto URL para el archivo PDF recibido
      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);

      // Crear un enlace temporal para descargar el archivo
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `reporte_orden_${orden_id}.pdf`); // Nombre del archivo
      document.body.appendChild(link);
      link.click();

      // Limpiar el enlace temporal
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      setMensaje(`Reporte de la orden ${orden_id} descargado exitosamente.`);
    } catch (err) {
      console.error("Error al descargar el reporte:", err.message);
      setError(`Error al descargar el reporte de la orden ${orden_id}.`);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Reportes de Órdenes</h2>

      {mensaje && <p style={styles.success}>{mensaje}</p>}
      {error && <p style={styles.error}>{error}</p>}

      {/* Listado de órdenes */}
      <h3>Órdenes Existentes</h3>
      {ordenes.length > 0 ? (
        <ul style={styles.list}>
          {ordenes.map((orden) => (
            <li key={orden.id} style={styles.listItem}>
              <div>
                <strong>ID:</strong> {orden.id} | <strong>Usuario ID:</strong>{" "}
                {orden.usuario_id} | <strong>Producto ID:</strong>{" "}
                {orden.producto_id} | <strong>Cantidad:</strong> {orden.cantidad} |{" "}
                <strong>Fecha de Entrega:</strong> {orden.fecha_entrega}
              </div>
              <button
                onClick={() => handleDescargarPDF(orden.id)}
                style={styles.button}
              >
                Descargar Reporte PDF
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay órdenes registradas.</p>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "800px",
    margin: "30px auto",
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
    backgroundColor: "#664242",
  },
  button: {
    backgroundColor: "#28a745",
    color: "#fff",
    padding: "8px 12px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "14px",
    marginTop: "10px",
  },
  success: { color: "green", marginTop: "10px" },
  error: { color: "red", marginTop: "10px" },
  list: { listStyleType: "none", padding: 0 },
  listItem: {
    padding: "10px",
    backgroundColor: "#23ff00",
    borderRadius: "5px",
    marginBottom: "10px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
};

export default Reportes;
