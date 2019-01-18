function editTunableParameter(modelName, varName, varValue)
    % Only use this function to change Simulink paremeters in the top level
    % model. This can't be used to change Matlab variables in the
    % referenced models.
    WS = get_param(modelName,'modelworkspace');
    TEMP = Simulink.Parameter;
    TEMP.Value = varValue;
    TEMP.CoderInfo.StorageClass = 'SimulinkGlobal';
    TEMP.CoderInfo.Alias = '';
    TEMP.CoderInfo.Alignment = -1;
    TEMP.CoderInfo.CustomStorageClass = 'Default';
    TEMP.Description = '';
    TEMP.DataType = class(varValue);
    TEMP.Min = [];
    TEMP.Max = [];
    TEMP.DocUnits = '';
    WS.assignin(varName,TEMP);
    clear WS TEMP
end

% IE: editTunableParameter('myModel','myVariable',0.349066);