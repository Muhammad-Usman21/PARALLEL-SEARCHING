import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import TextFiles from "../components/TextFiles";
import ExcelFiles from "../components/ExcelFiles";
import ResearchFiles from "../components/ResearchFiles";
import Sidebar from "../components/Sidebar";

const Home = () => {
	const location = useLocation();
	const [tab, setTab] = useState("");

	useEffect(() => {
		const urlParams = new URLSearchParams(location.search);
		const tabFromUrl = urlParams.get("tab");
		if (tabFromUrl) {
			setTab(tabFromUrl);
		}
	}, [location.search]);

	return (
		<div className="min-h-screen flex flex-col md:flex-row">
			<div className="md:w-64">
				<Sidebar />
			</div>
			{(tab === "text" || tab === "") && <TextFiles />}
			{tab === "excel" && <ExcelFiles />}
			{tab === "research" && <ResearchFiles />}
		</div>
	);
};

export default Home;
