import { Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import NotFound from "./pages/not-found";

function App() {
	return (
		<Routes>
			<Route path="/" element={<Home />} />
			{/* Add a catch-all route for 404 page */}
			<Route path="*" element={<NotFound />} />
		</Routes>
	);
}

export default App;
