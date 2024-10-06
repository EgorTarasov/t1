import { SkillEndpoint } from "@/api/endpoints/skill.endpoint";
import { observable } from "mobx";
import { observer } from "mobx-react-lite";
import { FC, useEffect } from "react";
import { SkillDto } from "@/api/models/skill.model";
import DropdownMultiple from "../DropdownMultiple";

interface Props {
  value: SkillDto.Item[];
  onChange: (value: SkillDto.Item[]) => void;
  label?: string;
  filter?: (value: SkillDto.Item) => boolean;
}

export const skillsStore = observable<{ skills: SkillDto.Item[] }>({
  skills: [],
});

export const SkillsDropdown: FC<Props> = observer((x) => {
  useEffect(() => {
    const fetchSkills = async () => {
      skillsStore.skills = await SkillEndpoint.list();
    };

    if (skillsStore.skills.length === 0) {
      fetchSkills();
    }
  }, []);

  const skills = x.filter
    ? skillsStore.skills.filter(x.filter)
    : skillsStore.skills;

  return (
    <DropdownMultiple
      label={x.label}
      value={x.value}
      onChange={x.onChange}
      options={skills}
      compare={(a) => a.name}
      render={(item) => item.name}
      placeholder="Выберите навыки"
    />
  );
});
