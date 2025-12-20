import auth_service from "../../api/auth.jsx";

export const Logout = () => {
    auth_service.logout();

    return <div>Всего хорошего!</div>
}