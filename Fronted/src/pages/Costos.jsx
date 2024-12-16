import { useState } from "react";
import { calcularCostos } from "../services/api";

const Costos = () => {
  const [cantidad, setCantidad] = useState("");
  const [modelo, setModelo] = useState("");
  const [fechaEntrega, setFechaEntrega] = useState("");
  const [resultados, setResultados] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResultados(null);

    try {
      // Preparar datos a enviar
      const data = {
        cantidad: parseInt(cantidad, 10),
        modelo,
        fecha_entrega: fechaEntrega,
      };

      // Llamada a la API
      const response = await calcularCostos(data);
      setResultados(response.data);
    } catch (err) {
      console.error("Error al calcular los costos:", err.message);
      setError("Hubo un error al calcular los costos. Inténtalo de nuevo.");
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Cálculo de Costos</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <label style={styles.label}>Cantidad del pedido:</label>
        <input
          type="number"
          placeholder="Ingrese la cantidad"
          value={cantidad}
          onChange={(e) => setCantidad(e.target.value)}
          style={styles.input}
          required
        />

        <label style={styles.label}>Modelo del producto:</label>
        <input
          type="text"
          placeholder="Ingrese el modelo"
          value={modelo}
          onChange={(e) => setModelo(e.target.value)}
          style={styles.input}
          required
        />

        <label style={styles.label}>Fecha de entrega:</label>
        <input
          type="date"
          value={fechaEntrega}
          onChange={(e) => setFechaEntrega(e.target.value)}
          style={styles.input}
          required
        />

        <button type="submit" style={styles.button}>
          Calcular Costos
        </button>
      </form>

      {error && <p style={styles.error}>{error}</p>}

      {resultados && (
        <div style={styles.resultados}>
          <h3>Resultados del Cálculo:</h3>
          <p><strong>Costo Total:</strong> ${resultados.costo_total}</p>
          <p><strong>Precio Unitario:</strong> ${resultados.precio_unitario}</p>
          <p><strong>Detalles:</strong> {resultados.detalle}</p>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "500px",
    margin: "30px auto",
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    boxShadow: "0px 4px 6px rgba(0,0,0,0.1)",
    backgroundColor: "#f9f9f9",
  },
  title: { textAlign: "center", marginBottom: "20px" },
  form: { display: "flex", flexDirection: "column", gap: "10px" },
  label: { fontWeight: "bold" },
  input: {
    padding: "8px",
    border: "1px solid #ccc",
    borderRadius: "5px",
  },
  button: {
    backgroundColor: "#28a745",
    color: "#fff",
    padding: "10px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  },
  error: { color: "red", marginTop: "10px" },
  resultados: {
    marginTop: "20px",
    padding: "10px",
    border: "1px solid #28a745",
    borderRadius: "5px",
    backgroundColor: "#e9ffe9",
  },
};

export default Costos;
