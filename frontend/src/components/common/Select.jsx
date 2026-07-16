function Select({

    value,

    onChange,

    options = []

}) {

    return (

        <select

            value={value}

            onChange={onChange}

            style={{

                width: "100%",

                padding: 12,

                borderRadius: 8,

                background: "#0f172a",

                color: "white",

                border: "1px solid #334155"

            }}

        >

            {

                options.map(option => (

                    <option

                        key={option.value}

                        value={option.value}

                    >

                        {option.label}

                    </option>

                ))

            }

        </select>

    );

}

export default Select;