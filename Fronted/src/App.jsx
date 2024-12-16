import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";
import Dashboard from "./pages/Dashboard";
import Costos from "./pages/Costos";
import Ordenes from "./pages/Ordenes";
import Reportes from "./pages/Reportes";
import Admin from "./pages/Admin/Admin";
import AdminProductos from "./pages/Admin/AdminProductos";
import AdminManoObra from "./pages/Admin/AdminManoObra";
import AdminMateriaPrima from "./pages/Admin/AdminMateriaPrima";
import AdminCostosIndirectos from "./pages/Admin/AdminCostosIndirectos";

function App() {
  return (
    <Router>
      <Routes>
        {/* Rutas sin Navbar */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Rutas con Navbar */}
        <Route
          path="*"
          element={
            <>
              <Navbar />
              <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/costos" element={<Costos />} />
                <Route path="/ordenes" element={<Ordenes />} />
                <Route path="/reportes" element={<Reportes />} />
                <Route path="/admin" element={<Admin />} />
                <Route path="/admin/productos" element={<AdminProductos />} />
                <Route path="/admin/mano-obra" element={<AdminManoObra />} />
                <Route path="/admin/materia-prima" element={<AdminMateriaPrima />} />
                <Route path="/admin/costos-indirectos" element={<AdminCostosIndirectos />} />
              </Routes>
            </>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
