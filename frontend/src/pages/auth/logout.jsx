import { useEffect } from "react";
import auth_service from "../../api/auth.jsx";

export const Logout = () => {

        const handletest = async () => {
            await auth_service.logout()
        }

        useEffect(() => {
            handletest();
        }, []);

    return <div>Всего хорошего!</div>
}
