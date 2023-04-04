import React, { useState } from 'react';
import axios from 'axios';
import 'bulma/css/bulma.min.css';


function App() {
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState('');
  const [questions, setQuestions] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [responseData, setResponseData] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileTypeChange = (event) => {
    setFileType(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    try {
      setResponseData(null)
      const formData = new FormData();
      formData.append('file', file);
      formData.append('document_type', fileType);
      formData.append('questions', questions);
      // formData.append('questions', "[\"name of establishment\", \"name of person owning the shop\", \"is this a valid shop establishment document in india? why?\"]");
      const response = await axios.post('https://cb37-103-158-140-208.in.ngrok.io/make_ocr_request', formData);
      console.log(response.data)
      setResponseData(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  function handleQuestionsChange(event) {
    setQuestions(event.target.value);
  }

  return (
      <div className="container">
        <nav className="navbar has-shadow"
             role="navigation"
             aria-label="main navigation">
          <div className="navbar-brand">
            <a className="navbar-item"
               href="https://bulma.io">
            <strong> KYC-GPT </strong>
            </a>

            <a role="button"
               className="navbar-burger"
               aria-label="menu"
               aria-expanded="false">
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
            </a>
          </div>
        </nav>
        <br/><br/>
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label className="label">Choose a file:</label>
            <div className="control">
              <input className="input" type="file" onChange={handleFileChange} />
            </div>
          </div>
          <div className="field">
            <label className="label">Choose a Document type:</label>
            <div className="control">
              <div className="select">
                <select value={fileType} onChange={handleFileTypeChange}>
                  <option value="">--Please choose an option--</option>
                  <option value="unknown">Unknown</option>
                  <option value="shop_establishment">shop_establishment</option>
                  <option value="partnership_deed">partnership_deed</option>
                </select>
              </div>
            </div>
          </div>
          {
          fileType === 'unknown' &&
          <div className="field">
            <label className="label">Type comma seperated questions</label>
            <div className="control">
                <textarea onChange={handleQuestionsChange} className="textarea" placeholder="e.g. name of establishment, name of person owning the shop, is this a valid shop establishment document in india? why?"></textarea>
            </div>
          </div>
          }
          <div className="field">
            <div className="control">
              <button className="button is-primary" type="submit">
                {isLoading ? 'Loading...' : 'Submit'}
              </button>
            </div>
          </div>
        </form>
        <br />
        <br />




        <div className="columns">
          <div className="column is-half">
        {responseData && (
         <>
            <h2 className="heading" style={
              {
                fontSize: "20px",
              }
            }>Result: </h2>
            <table className="table">
              <tbody>
              {Object.keys(responseData).map((key) => (
                  <>
                    <tr>
                  <th key={key}>{key}</th>
                  <td key={key}>
                    {responseData[key]}
                  </td>
                    </tr>
                  </>
              ))}
              </tbody>
            </table>
         </>
        )}
          </div>
      <div className="column is-half">
        {file && responseData && (
            <div>
              <h2 className="heading">Uploaded Image/PDF: </h2>
              {fileType != 'partnership_deed' && (
                  <>
                    <img src={URL.createObjectURL(file)} alt="uploaded" />
                  </>
              )}

              {fileType === 'partnership_deed' && (
                  <div>
                    <embed src={URL.createObjectURL(file)} type="application/pdf" width="100%" height="600px" />
                  </div>
              )}ls
            </div>
        )}
      </div>
        </div>

      </div>
  );
}

// test for App


export default App;
