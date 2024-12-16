import axios from "axios";

// Configuración de Axios
const API = axios.create({
  baseURL: "http://localhost:5000", // Asegúrate de usar la URL de tu backend
});

// Interceptor para incluir el token en las solicitudes protegidas
API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

// ----- FUNCIONES PARA LA API -----

// --- USUARIOS ---
export const login = (data) => API.post("/usuarios/login", data);
export const register = (data) => API.post("/usuarios/registro", data);
export const getRolUsuario = () => API.get("/usuarios/rol");

// --- PRODUCTOS ---
export const crearProducto = (data) => API.post("/productos/crear", data);
export const getProductos = () => API.get("/productos/getAll");
export const actualizarProducto = (data) => API.put("/productos/actualizar", data);
export const eliminarProducto = (id) =>
  API.delete("/productos/eliminar", { data: { id } });

// --- MANO DE OBRA ---
export const crearManoObra = (data) => API.post("/mano-obra/post", data);
export const getManoObra = () => API.get("/mano-obra/getAll");
export const actualizarManoObra = (id, data) =>
  API.put(`/mano-obra/put/${id}`, data);
export const eliminarManoObra = (id) => API.delete(`/mano-obra/delete/${id}`);

// --- MATERIA PRIMA ---
export const crearMateriaPrima = (data) => API.post("/materia-prima/post", data);
export const getMateriaPrima = () => API.get("/materia-prima/getAll");
export const actualizarMateriaPrima = (id, data) =>
  API.put(`/materia-prima/put/${id}`, data);
export const eliminarMateriaPrima = (id) =>
  API.delete(`/materia-prima/delete/${id}`);

// --- COSTOS INDIRECTOS ---
// Obtener todos los costos indirectos
export const getCostosIndirectos = () => API.get("/costos-indirectos/getAll");

// Crear nuevo costo indirecto
export const crearCostoIndirecto = (data) => API.post("/costos-indirectos/post", data);

// Actualizar un costo indirecto
export const actualizarCostoIndirecto = (id, data) => API.put(`/costos-indirectos/put/${id}`, data);

// Eliminar un costo indirecto
export const eliminarCostoIndirecto = (id) => API.delete(`/costos-indirectos/delete/${id}`);

// --- ORDENES DE PEDIDO ---
export const crearOrden = (data) => API.post("/ordenes-pedido/post", data);
export const getOrdenes = () => API.get("/ordenes-pedido/getAll");
export const actualizarOrden = (id, data) =>
  API.put(`/ordenes-pedido/put/${id}`, data);
export const eliminarOrden = (id) =>
  API.delete(`/ordenes-pedido/delete/${id}`);

// --- COSTOS CALCULADOS ---
export const calcularCostos = (data) => API.post("/costos/calcular", data);

// --- REPORTES (PDF) ---
export const descargarReportePDF = () =>
  API.get("/ordenes-pedido/pdf", { responseType: "blob" });

// Exportar todas las funciones juntas
export default {
  login,
  register,
  getRolUsuario,
  crearProducto,
  getProductos,
  actualizarProducto,
  eliminarProducto,
  crearManoObra,
  getManoObra,
  actualizarManoObra,
  eliminarManoObra,
  crearMateriaPrima,
  getMateriaPrima,
  actualizarMateriaPrima,
  eliminarMateriaPrima,
  getCostosIndirectos,
  crearCostoIndirecto,
  actualizarCostoIndirecto,
  eliminarCostoIndirecto,
  crearOrden,
  getOrdenes,
  actualizarOrden,
  eliminarOrden,
  calcularCostos,
  descargarReportePDF,
};
