import { useEffect } from "react";
import { auth_service } from "../api/auth";

export const TestPage = () => {

    const handletest = async () => {
        console.log(await auth_service.status())
    }

    useEffect(() => {
        handletest();
    }, []);

    return <div>Опа а это тестовая инфа</div>
};
