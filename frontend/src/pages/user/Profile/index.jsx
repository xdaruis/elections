import axios from 'axios';
import React, { useEffect, useState } from 'react';

import CustomCard from '../../../components/ui/CustomCard';
import CustomInput from '../../../components/ui/CustomInput';
import ErrorCard from '../../../components/ui/ErrorCard';
import InfoText from '../../../components/ui/InfoText';
import Loader from '../../../components/ui/Loader';
import getError from '../../../utils/getError';

function Profile() {
  const [formData, setFormData] = useState({});
  const [changes, setChanges] = useState({});
  const [fetchError, setFetchError] = useState('');
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfileData = async () => {
      if (localStorage.token) {
        try {
          const { data } = await axios.get('/api/user/profile/');
          setFormData(data);
          setChanges(data);
        } catch (err) {
          setFetchError(getError(err));
        } finally {
          setLoaded(true);
        }
      }
    };
    fetchProfileData();
  }, []);

  if (!loaded) return <Loader />;

  if (fetchError) return <ErrorCard message={fetchError} />;

  const handleSave = async () => {
    try {
      await axios.put('/api/user/profile/', changes);
      setFormData(changes);
    } catch (err) {
      setError(getError(err));
    }
  };

  const hasChanges = () => JSON.stringify(formData) !== JSON.stringify(changes);

  return (
    <CustomCard title="User Profile" width="3">
      <InfoText message={error} type="error" />
      {Object.keys(formData).length > 0 &&
        Object.entries(changes).map(([key, value]) => (
          <CustomInput
            id={key}
            setData={setChanges}
            label={key.charAt(0).toUpperCase() + key.slice(1)}
            type="text"
            value={value}
          />
        ))}
      {hasChanges() && (
        <div className="mt-3">
          <button
            type="button"
            className="btn btn-primary me-2"
            onClick={handleSave}
          >
            Save Changes
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => setChanges(formData)}
          >
            Cancel
          </button>
        </div>
      )}
    </CustomCard>
  );
}

export default Profile;
