import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Home from "./pages/Home";

const App = () => {
	return (
		<BrowserRouter>
			<Header />
			<Routes>
				<Route path="/" element={<Home />} />
			</Routes>
		</BrowserRouter>
	);
};

export default App;
