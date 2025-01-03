import { Button, Navbar } from "flowbite-react";
import { Link } from "react-router-dom";
import { HiMoon, HiSun } from "react-icons/hi";
import { useSelector, useDispatch } from "react-redux";
import { toggleTheme } from "../redux/theme/themeSlice";

const Header = () => {
	const dispatch = useDispatch();
	const { theme } = useSelector((state) => state.theme);

	return (
		<Navbar className="border-b-2 border-teal-600 lg:px-14 bg-cover bg-center sticky top-0 z-30 bg-[url('../../h&f-light.jpg')] dark:bg-[url('../../header-dark.jpg')]">
			<Link
				to="/?tab=text"
				className="font-semibold dark:text-white flex items-center">
				<span className="text-xl sm:3xl uppercase">Searching</span>
			</Link>
			<Button
				className="w-8 h-8 sm:w-10 sm:h-10 focus:ring-1 items-center bg-transparent border-teal-400"
				color="gray"
				pill
				onClick={() => dispatch(toggleTheme())}>
				{theme === "light" ? <HiMoon /> : <HiSun />}
			</Button>
		</Navbar>
	);
};

export default Header;
