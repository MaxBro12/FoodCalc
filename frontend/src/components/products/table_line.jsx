import { not_to_long_text } from "@/components/utils/string_line.jsx";


export const ProductLine = ({data, update, action_on_click}) => {
    const handle_click = () => {
        action_on_click(data)
    }
    return <tr onClick={() => handle_click()}>
        <td className='desktop' style={{userSelect:'none'}} dangerouslySetInnerHTML={{__html: not_to_long_text(data.name, '', 100)}}></td>
        <td className='desktop' style={{userSelect:'none'}} dangerouslySetInnerHTML={{__html: not_to_long_text('', data.description, 100)}}></td>
    </tr>
}
