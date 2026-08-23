import '../styles/sidebar.css';
import api from '../src/api.js';
import { useState, useEffect } from 'react';
import closeIcon from '../src/assets/close.svg';

export default function Sidebar({inputs, setInputs, solve}) {
  const [activeIndex, setActiveIndex] = useState(-1);
  const [resources, setResources] = useState([]);

  useEffect(() => {
    fetchResources('').then((data) =>
      setResources(data));
  }, [])

  async function fetchResources(query) {
    try {
      const res = await api.get('/search-resources', {
        params: {
          input: query
        }
      });
      setResources(res.data);
    } catch (e) {
      console.error('Error fetching resources', e);
    }
  }

  function addInput() {
    setInputs([
      ...inputs,
      {
        resource: '',
        amount: ''
      }
    ]);
  }

  function updateInput(index, value) {
    const newInputs = [...inputs];
    newInputs[index].resource = value.toLowerCase();
    setInputs(newInputs);
  }

  function updateAmount(index, value) {
    const numberRe = /^\d*\.?\d*$/;
    if (numberRe.test(value)) {
      const newInputs = [...inputs];
      newInputs[index].amount = value;
      setInputs(newInputs);
    }
  }

  function deleteInput(index) {
    const newInputs = [...inputs];
    if (index >= 0)
      newInputs.splice(index, 1);
    setInputs(newInputs);
  }

  function handleBlur() {
    setTimeout(() =>
      setActiveIndex(-1)
    , 200);
  }

  return (
    <div className='sidebar'>
      <p className='inputs-title'>Inputs</p>
      <ul className='inputs'>
        {inputs.map((input, index) =>
          <li key={index}>
            <input
              type='text'
              value={input.resource}
              placeholder='Enter resource'
              className='resource-input'
              onClick={() => setActiveIndex(index)}
              onBlur={() => handleBlur()}
              onChange={(e) => updateInput(index, e.target.value)}
            >
            </input>
            <input
              type='text'
              inputMode='numeric'
              value={input.amount}
              placeholder='0'
              className='amount-input'
              onChange={(e) => updateAmount(index, e.target.value)}
            />
            <img className='delete' src={closeIcon} onClick={() => deleteInput(index)} />
          </li>
        )}
      </ul>
      <button className='add-input' onClick={() => addInput()}>+ Add Input</button>
      <button className='solve-button' onClick={() => solve()}>Solve</button>
    </div>
  )
}