import { Sidebar } from "flowbite-react";
import { useEffect, useState } from "react";
import { HiAcademicCap, HiDocumentText, HiTable, HiUser } from "react-icons/hi";

import { Link, useLocation } from "react-router-dom";

import { useSelector } from "react-redux";

const DashSidebar = () => {
	const location = useLocation();
	const [tab, setTab] = useState("");
	const { theme } = useSelector((state) => state.theme);

	useEffect(() => {
		const urlParams = new URLSearchParams(location.search);
		const tabFromUrl = urlParams.get("tab");
		if (tabFromUrl) {
			setTab(tabFromUrl);
		}
	}, [location.search]);

	return (
		<Sidebar className={`w-full md:w-64 ${theme}`}>
			<Sidebar.Items>
				<Sidebar.ItemGroup className="flex flex-col">
					<Link to="/?tab=text">
						<Sidebar.Item
							active={tab === "text" || tab === ""}
							icon={HiDocumentText}
							as="div">
							Pattern Searching
						</Sidebar.Item>
					</Link>
					<Link to="/?tab=excel">
						<Sidebar.Item active={tab === "excel"} icon={HiTable} as="div">
							Excel Files
						</Sidebar.Item>
					</Link>
					<Link to="/?tab=research">
						<Sidebar.Item
							active={tab === "research"}
							icon={HiAcademicCap}
							as="div">
							Research Papers
						</Sidebar.Item>
					</Link>
				</Sidebar.ItemGroup>
			</Sidebar.Items>
		</Sidebar>
	);
};

export default DashSidebar;
