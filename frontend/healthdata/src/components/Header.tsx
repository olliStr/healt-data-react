import { useState, useEffect } from "react";
import {  Navbar,   NavbarBrand,   NavbarContent,   NavbarItem,   NavbarMenuToggle,  NavbarMenu,  NavbarMenuItem} from "@nextui-org/navbar";
import { Button } from "@nextui-org/button";

const Header = () => {
    const [darkMode, setDarkMode] = useState(false);

    useEffect(() => {
        if (darkMode) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }, [darkMode])

    return (
        <Navbar>
            <NavbarContent>
                <p className="text-lg">Health Data App</p>
            </NavbarContent>
            <NavbarItem>
                <Button
                    className="ml-auto"
                    onClick={() => setDarkMode(!darkMode)}
                    >
                    {darkMode ? 'Light Mode' : 'Dark Mode'}
                </Button>
            </NavbarItem>
        </Navbar>

    )
}

export default Header