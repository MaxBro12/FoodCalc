import { useState } from 'react';
import { useNavigate } from "react-router-dom";

import db_service from "@/api/universe.jsx";
import PaginationTable from "@/components/utils/custom_tables.jsx";

import { ProductDetail } from '@/components/products/table_detail.jsx'
import { ProductsHeader } from '@/components/products/table_header.jsx'
import { ProductLine } from '@/components/products/table_line.jsx'


export const ProductsPage = () => {
    const navigate = useNavigate()
    const [show_new, set_show_new] = useState(false);

    return <div style={{
        padding: 5,
        height: '100%',
        width: '100%',
        maxWidth: '50em',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'flex-start',
    }}>
        <button className='rounded_border base_margins' onClick={() => set_show_new(true)} style={{
            marginBottom: 5
        }}>Создать новое</button>
        <PaginationTable CustomHead={ProductsHeader} Line={ProductLine} Detail={ProductDetail} api_request={db_service.products.all}/>
    </div>
}
