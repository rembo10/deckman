import React from "react";

interface Profile {
  id: number;
  name: string;
  position: number;
}

interface ProfileEditorProps {
  profiles?: Profile[]
}

export const ProfileEditor = ({
  profiles = []
}: ProfileEditorProps) => {
  return (
    <div>
      <h1>Profiles</h1>
      <ul>
        { profiles.map(p => (<li>{p.name}</li>)) }
      </ul>
      <button>Add New</button>
    </div>
  )
}

export default ProfileEditor;
